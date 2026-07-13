using UnityEngine;

public class Turbines : MonoBehaviour
{
	public GameObject turbine2;

	public GameObject turbine3;

	public GameObject debris2;

	public GameObject debris3;

	private Airport airport;

	private void Start()
	{
		airport = Singleton<AirportManager>.Instance.GetClosestAirport(base.transform.position);
	}

	private void Update()
	{
		turbine2.SetActive(airport.allQuests[1].completed || !StoryState.postEarthquake);
		debris2.SetActive(!airport.allQuests[1].completed && StoryState.postEarthquake);
		turbine3.SetActive(airport.allQuests[2].completed || !StoryState.postEarthquake);
		debris3.SetActive(!airport.allQuests[2].completed && StoryState.postEarthquake);
	}
}
