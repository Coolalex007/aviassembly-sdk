using UnityEngine;

public class EarthquakeBreakObject : MonoBehaviour
{
	public Rigidbody rb;

	private void Start()
	{
		rb.useGravity = false;
	}

	private void Update()
	{
		if (StoryState.earthquakeStarted && !StoryState.postEarthquake)
		{
			rb.useGravity = true;
		}
	}
}
