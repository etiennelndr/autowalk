using UnityEngine;
using UnityEngine.AI;

public enum Behaviour {
    TRAINING,
    PATROLLING
}

public class Walker : MonoBehaviour {
    [SerializeField]
    private string serverURL;

    [SerializeField]
    private Behaviour behaviour;

    [SerializeField]
    private TrainingAgentConfig trainingAgentConfig;

    [SerializeField]
    private PatrollingAgentConfig patrollingAgentConfig;

    private BaseAgent agent;

    // Start is called before the first frame update
    void Start() {
        var navMeshAgent = GetComponent<NavMeshAgent>();

        if (behaviour == Behaviour.TRAINING) {
            Debug.Log(trainingAgentConfig);
            agent = new TrainingAgent(trainingAgentConfig, gameObject);
        }
        else if (behaviour == Behaviour.PATROLLING) {
            Debug.Log(patrollingAgentConfig);
            agent = new PatrollingAgent(patrollingAgentConfig, gameObject);
        }

        agent.Init();
    }

    // Update is called once per frame
    void Update() {
        agent.Move();
    }
}
