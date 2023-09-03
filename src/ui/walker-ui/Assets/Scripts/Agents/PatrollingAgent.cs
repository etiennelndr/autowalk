using System;
using UnityEngine;

[Serializable]
public class PatrollingAgentConfig : BaseAgentConfig {
    public string serverURL;
}

public class PatrollingAgent : BaseAgent<PatrollingAgentConfig> {
    public PatrollingAgent(PatrollingAgentConfig config, GameObject linkedGO) : base(config, linkedGO) {
    }

    public override void Init() {
        Debug.Log("Patrolling agent: Init");
    }

    public override void Move() {
        Debug.Log("Training agent: Move");
    }
}
