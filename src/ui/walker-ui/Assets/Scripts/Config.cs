using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Config : MonoBehaviour {
    [SerializeField]
    private int frameRate = 10;

    [SerializeField]
    private int vSyncCount = 1;

    // Start is called before the first frame update
    void Start() {
        Application.targetFrameRate = frameRate;
        QualitySettings.vSyncCount = vSyncCount;
    }
}
