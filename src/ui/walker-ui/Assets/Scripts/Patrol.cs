using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using Unity.VisualScripting;
using UnityEditorInternal;
using UnityEngine;
using UnityEngine.AI;
using static UnityEngine.GraphicsBuffer;

public class Patrol : MonoBehaviour {
    private NavMeshAgent agent;

    [SerializeField]
    private float remainingDistanceTolerance = 2f;

    [SerializeField]
    private Transform[] targetPoints;

    [SerializeField]
    private bool drawTargetPoints = false;

    private Vector3 currentTargetPoint;
    private Vector3 previousTargetPoint;

    private readonly System.Random rnd = new System.Random();

    // Start is called before the first frame update
    void Start() {
        agent = GetComponent<NavMeshAgent>();

        // Disabling auto-braking allows for continuous movement
        // between points (ie, the agent doesn't slow down as it
        // approaches a destination point).
        agent.autoBraking = false;

        UpdateTarget();
    }

    // Update is called once per frame
    void Update() {
        // Choose the next destination point when the agent gets close to the current one.
        if (!agent.pathPending && agent.remainingDistance < remainingDistanceTolerance)
            UpdateTarget();

        if (drawTargetPoints)
            DrawTargetPoints();
    }

    void UpdateTarget() {
        // Returns if no points have been set up
        if (targetPoints.Length == 0)
            return;

        // Choose the next point in the array
        Vector3 newTargetPoint = GetNextTargetPoint();
        // Set the agent to go to the currently selected target
        agent.SetDestination(newTargetPoint);
        // Save previous and new target points for next update
        previousTargetPoint = currentTargetPoint;
        currentTargetPoint = newTargetPoint;
    }

    Vector3 GetNextTargetPoint() {
        // Returns the first point if no target is set (i.e. point selected at startup)
        if (currentTargetPoint == null) {
            Debug.Log("No target point set, defaulting to the first point available");
            return targetPoints[0].position;
        }

        // Retrieve each point with no collider intersecting a line between it and the current target
        List<Vector3> nextPoints = new List<Vector3>();
        foreach (var point in targetPoints) {
            var pointPosition = point.position;
            // Always exclude the previous and current target points
            if (
                pointPosition == currentTargetPoint
                || pointPosition == previousTargetPoint
                || Physics.Linecast(currentTargetPoint, pointPosition)
            ) {
                continue;
            }
            nextPoints.Add(pointPosition);
        }

        // When no points are "visible", select a random one in the global list of points
        if (nextPoints.Count == 0) {
            Debug.LogError("Unable to find any visible target point(s), defaulting to a random one");
            nextPoints = targetPoints
                // Exclude the previous and current target points
                .Where(p => p.position != currentTargetPoint && p.position != previousTargetPoint)
                .Select(p => p.position)
                .ToList();
        }
        else {
            Debug.Log("Found " + nextPoints.Count + " new target point(s)");
        }

        int nextPointIndex = rnd.Next(nextPoints.Count);
        return nextPoints[nextPointIndex];
    }

    void DrawTargetPoints() {
        foreach (var targetPoint in targetPoints) {
            var targetPointPosition = targetPoint.position;
            if (targetPointPosition == currentTargetPoint) {
                Debug.DrawRay(targetPointPosition, transform.up * 2.5f, Color.green);
            }
            else if (targetPointPosition == previousTargetPoint) {
                Debug.DrawRay(targetPointPosition, transform.up * 2.5f, Color.blue);
            }
            else {
                Debug.DrawRay(targetPointPosition, transform.up * 2.5f, Color.black);
            }
        }
    }
}
