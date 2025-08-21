import HashMap "mo:base/HashMap";
import Principal "mo:base/Principal";
import Nat "mo:base/Nat";
import Iter "mo:base/Iter";
import Array "mo:base/Array";

persistent actor {

  var stableData : [(Principal, [Nat])] = [];

  transient let eqP = Principal.equal;
  transient let hashP = Principal.hash;
  transient var store = HashMap.HashMap<Principal, [Nat]>(16, eqP, hashP);

  system func preupgrade() {
    stableData := Iter.toArray(store.entries());
  };

  system func postupgrade() {
    store := HashMap.HashMap<Principal, [Nat]>(stableData.size(), eqP, hashP);
    for ((p, list) in stableData.vals()) {
      store.put(p, list);
    };
    stableData := [];
  };

  func getOrInit(caller : Principal) : [Nat] {
    switch (store.get(caller)) {
      case (?list) list;
      case null {
        store.put(caller, []);
        []
      }
    }
  };

  public shared ({ caller }) func addProposalId(id : Nat) : async () {
    let list = getOrInit(caller);
    if (Array.find<Nat>(list, func(x) { x == id }) == null) {
      store.put(caller, Array.append<Nat>(list, [id]));
    };
  };

  public shared ({ caller }) func removeProposalId(id : Nat) : async () {
    let list = getOrInit(caller);
    let updated = Array.filter<Nat>(list, func(x) { x != id });
    store.put(caller, updated);
  };

  public query ({ caller }) func getProposalIds() : async [Nat] {
    getOrInit(caller)
  };
};
