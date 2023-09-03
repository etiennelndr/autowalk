using UnityEngine;

public abstract class BaseAgentConfig {
}

public abstract class BaseAgent<C> where C: BaseAgentConfig {
    protected C config;
    protected GameObject linkedGO;

    public BaseAgent(C config, GameObject linkedGO) {
        this.config = config;
        this.linkedGO = linkedGO;
    }

    public abstract void Init();

    public abstract void Move();
}
