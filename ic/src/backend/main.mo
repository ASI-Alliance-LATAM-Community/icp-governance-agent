import HashMap  "mo:base/HashMap";
import Principal "mo:base/Principal";
import Text      "mo:base/Text";
import Time      "mo:base/Time";
import Nat64     "mo:base/Nat64";
import Iter      "mo:base/Iter";

persistent actor {

  public type UserPrefs = {
    include_topic         : [Text];
    include_status        : [Text];
    include_action        : [Text];
    include_reward_status : [Text];
    manage_neuron_id      : ?Nat;
    proposer              : ?Nat;
  };

  public type UserState = {
    prefs                  : UserPrefs;
    last_seen_proposal_id  : ?Nat;
    webhook                : ?Text;
    created_at_ns          : Nat64;
    updated_at_ns          : Nat64;
  };

  var stableEntries : [(Principal, UserState)] = [];

  transient let eqP   = Principal.equal;
  transient let hashP = Principal.hash;

  transient var store = HashMap.HashMap<Principal, UserState>(16, eqP, hashP);

  func now() : Nat64 = Nat64.fromIntWrap(Time.now());

  transient let emptyPrefs : UserPrefs = {
    include_topic = [];
    include_status = [];
    include_action = [];
    include_reward_status = [];
    manage_neuron_id = null;
    proposer = null;
  };

  func getOrInit(p : Principal) : UserState {
    switch (store.get(p)) {
      case (?s) s;
      case null {
        let ts = now();
        let s : UserState = {
          prefs = emptyPrefs;
          last_seen_proposal_id = null;
          webhook = null;
          created_at_ns = ts;
          updated_at_ns = ts;
        };
        store.put(p, s);
        s
      }
    }
  };

  system func preupgrade() {
    stableEntries := Iter.toArray(store.entries());
  };

  system func postupgrade() {
    store := HashMap.HashMap<Principal, UserState>(stableEntries.size(), eqP, hashP);
    for ((p, s) in stableEntries.vals()) { store.put(p, s) };
    stableEntries := [];
  };

  public query func version() : async Text { "icp-governance-prefs@1.0.0" };

  public shared ({ caller }) func setPrefs(prefs : UserPrefs) : async UserState {
    let ts = now();
    let old = getOrInit(caller);
    let s : UserState = {
      prefs = prefs;
      last_seen_proposal_id = old.last_seen_proposal_id;
      webhook = old.webhook;
      created_at_ns = old.created_at_ns;
      updated_at_ns = ts;
    };
    store.put(caller, s);
    s
  };

  public query ({ caller }) func getPrefs() : async ?UserPrefs {
    switch (store.get(caller)) { case (?s) ?s.prefs; case null null }
  };

  public shared ({ caller }) func setLastSeenProposalId(id : Nat) : async UserState {
    let ts = now();
    let old = getOrInit(caller);
    let s : UserState = {
      prefs = old.prefs;
      last_seen_proposal_id = ?id;
      webhook = old.webhook;
      created_at_ns = old.created_at_ns;
      updated_at_ns = ts;
    };
    store.put(caller, s);
    s
  };

  public query ({ caller }) func getLastSeenProposalId() : async ?Nat {
    switch (store.get(caller)) { case (?s) s.last_seen_proposal_id; case null null }
  };

  public shared ({ caller }) func setWebhook(url : ?Text) : async UserState {
    let ts = now();
    let old = getOrInit(caller);
    let s : UserState = {
      prefs = old.prefs;
      last_seen_proposal_id = old.last_seen_proposal_id;
      webhook = url;
      created_at_ns = old.created_at_ns;
      updated_at_ns = ts;
    };
    store.put(caller, s);
    s
  };

  public query ({ caller }) func getWebhook() : async ?Text {
    switch (store.get(caller)) { case (?s) s.webhook; case null null }
  };

  public shared ({ caller }) func getMyState() : async UserState {
    getOrInit(caller)
  };
}
