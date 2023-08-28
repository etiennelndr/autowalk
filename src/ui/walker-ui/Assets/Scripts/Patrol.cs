using System.Collections.Generic;
using System.Linq;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.AI;

public class Patrol : MonoBehaviour {
    private NavMeshAgent agent;

    [SerializeField]
    private float remainingDistanceTolerance = 2f;

    [SerializeField]
    private Transform[] targetPoints;

    [SerializeField]
    private bool targetPointsVisible = false;

    [SerializeField]
    private float targetPointsHeight = 2.5f;

    private Vector3 currentTargetPoint;
    private Vector3 previousTargetPoint;
    private List<Vector3> nextTargetPoints;

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

        if (targetPointsVisible)
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
        // Retrieve next target points for debugging purposes
        nextTargetPoints = GetVisiblePoints(currentTargetPoint);
    }

    Vector3 GetNextTargetPoint() {
        List<Vector3> nextPoints;
        // Returns the first point if no target is currently set (i.e. point selected at startup)
        if (currentTargetPoint == Vector3.zero) {
            Debug.Log("No target point set, defaulting to the first point available");
            nextPoints = GetVisiblePoints(agent.transform.position);
        }
        else {
            // Retrieve each point with no collider intersecting a line between it and the current target
            nextPoints = GetVisiblePoints(currentTargetPoint);

            // When no points are "visible", select a random one in the global list of points
            if (nextPoints.Count == 0) {
                Debug.LogError("Unable to find any visible target point(s), defaulting to a random one");
                nextPoints = targetPoints.Select(p => p.position).ToList();
            }
            else {
                Debug.Log("Found " + nextPoints.Count + " new target point(s)");
            }

            // Exclude the previous and current target points
            nextPoints = nextPoints.Where(p => p != currentTargetPoint && p != previousTargetPoint).ToList();
        }

        int nextPointIndex = rnd.Next(nextPoints.Count);
        return nextPoints[nextPointIndex];
    }

    List<Vector3> GetVisiblePoints(Vector3 point) {
        List<Vector3> visiblePoints = new List<Vector3>();
        foreach (var targetPoint in targetPoints) {
            var targetPointPosition = targetPoint.position;
            // If the current target point is the input point,
            if (targetPointPosition == point
                // or the point is hidden by an object,
                || Physics.Linecast(targetPointPosition, point)
                // or the distance between the two points is less than the required tolerance
                || Vector3.Distance(targetPointPosition, point) < remainingDistanceTolerance
            ) {
                // then, ignore this point
                continue;
            }
            visiblePoints.Add(targetPointPosition);
        }
        return visiblePoints;
    }

    void DrawTargetPoints() {
        foreach (var targetPoint in targetPoints) {
            var targetPointPosition = targetPoint.position;

            if (targetPointPosition == currentTargetPoint) {
                Debug.DrawRay(targetPointPosition, transform.up * targetPointsHeight, Color.green);
            }
            else if (targetPointPosition == previousTargetPoint) {
                Debug.DrawRay(targetPointPosition, transform.up * targetPointsHeight, Color.blue);
            }
            else if (nextTargetPoints.Contains(targetPointPosition)) {
                Debug.DrawRay(targetPointPosition, transform.up * targetPointsHeight, Color.yellow);
            }
            else {
                Debug.DrawRay(targetPointPosition, transform.up * targetPointsHeight, Color.black);
            }
        }
    }
}
