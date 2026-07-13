using System.Collections.Generic;
using UnityEngine;

public class ThottleUI : MonoBehaviour
{
	public GameObject throttleUIPrefab;

	public Transform uiParent;

	private List<Engine> engines = new List<Engine>();

	private List<ThrottleUIElement> throttleUI = new List<ThrottleUIElement>();

	private void Start()
	{
		List<string> list = new List<string>();
		Engine[] componentsInChildren = Singleton<PlaneContainer>.Instance.gameObject.GetComponentsInChildren<Engine>();
		for (int i = 0; i < componentsInChildren.Length; i++)
		{
			string item = componentsInChildren[i].GetControlScemeID() + componentsInChildren[i].useAfterburner;
			if (!list.Contains(item) || Vector3.Dot(componentsInChildren[i].GetDirection(), Singleton<PlaneContainer>.Instance.transform.up) > 0.99f)
			{
				if (!list.Contains(item) && Vector3.Dot(componentsInChildren[i].GetDirection(), Singleton<PlaneContainer>.Instance.transform.up) <= 0.99f)
				{
					list.Add(item);
				}
				engines.Add(componentsInChildren[i]);
				GameObject obj = Object.Instantiate(throttleUIPrefab);
				obj.transform.parent = uiParent;
				obj.transform.localScale = Vector3.one;
				obj.transform.SetAsFirstSibling();
				ThrottleUIElement componentInChildren = obj.GetComponentInChildren<ThrottleUIElement>();
				throttleUI.Add(componentInChildren);
				componentInChildren.InitKey("Throttle " + ((i > 0) ? i.ToString() : ""), componentsInChildren[i].GetKey1Path(), componentsInChildren[i].GetKey2Path(), componentsInChildren[i].useAfterburner);
			}
		}
	}

	private void Update()
	{
		for (int i = 0; i < engines.Count; i++)
		{
			throttleUI[i].UpdateValue(engines[i].currentThrottle);
		}
	}
}
