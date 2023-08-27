using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using Unity.VisualScripting;
using UnityEditorInternal;
using UnityEngine;
using UnityEngine.AI;
using static UnityEngine.GraphicsBuffer;

public class Patrol : MonoBehaviour
{
    private NavMeshAgent agent;

    [SerializeField]
    private float remainingDistanceTolerance = 0.5f; 

    [SerializeField]
    private Transform[] points;

    private Vector3 targetPoint;
    private Vector3 previousPoint;

    private readonly System.Random rnd = new System.Random();

    // Start is called before the first frame update
    void Start()
    {
        agent = GetComponent<NavMeshAgent>();

        // Disabling auto-braking allows for continuous movement
        // between points (ie, the agent doesn't slow down as it
        // approaches a destination point).
        agent.autoBraking = false;

        UpdateTarget();
    }

    // Update is called once per frame
    void Update()
    {
        // Choose the next destination point when the agent gets close to the current one.
        if (!agent.pathPending && agent.remainingDistance < remainingDistanceTolerance)
            UpdateTarget();

        Debug.DrawRay(targetPoint, new Vector3(targetPoint.x, targetPoint.y + 10, targetPoint.z), Color.blue);
    }

    void UpdateTarget()
    {
        // Returns if no points have been set up
        if (points.Length == 0)
            return;

        // Choose the next point in the array
        Vector3 newTargetPoint = GetNextTargetPoint();
        // Set the agent to go to the currently selected target
        agent.SetDestination(newTargetPoint);


        previousPoint = targetPoint;
        targetPoint = newTargetPoint;
    }

    Vector3 GetNextTargetPoint()
    {
        // Returns the first point if no target is set (i.e. point selected at startup)
        if (targetPoint == null)
        {
            Debug.Log("No target point set, defaulting to the first point available");
            return points[0].position;
        }

        // Retrieve each point with no collider intersecting a line between it and the current target
        List<Vector3> nextPoints = new List<Vector3>();
        foreach (var point in points)
        {
            var pointPosition = point.position;
            if (
                pointPosition == targetPoint
                || pointPosition == previousPoint
                || Physics.Linecast(targetPoint, pointPosition)
            ) {
                continue;
            }
            nextPoints.Add(pointPosition);
        }

        if (nextPoints.Count == 0)
        {
            Debug.LogError("Unable to find any visible target point(s), defaulting to a random one");
            nextPoints = points.Select(p => p.position).ToList(); 
        } else
        {
            Debug.Log("Found " + nextPoints.Count + " new target point(s)");
        }

        int nextPointIndex = rnd.Next(nextPoints.Count);
        return nextPoints[nextPointIndex];
    }
}
