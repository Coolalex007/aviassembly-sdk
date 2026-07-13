using TMPro;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.UI;

public class ThrottleUIElement : MonoBehaviour
{
	public TMP_Text throttleName;

	public TMP_Text throttleKeys;

	public Slider slider;

	public GameObject breakReverse;

	public GameObject afterBurner;

	public void InitKey(string throttleName, string keyPath1, string keyPath2, bool afterBurner)
	{
		this.throttleName.text = throttleName;
		throttleKeys.text = "( " + InputSystem.FindControl(keyPath1).displayName + " , " + InputSystem.FindControl(keyPath2).displayName + " )";
		this.afterBurner.SetActive(afterBurner);
	}

	public void UpdateValue(float value)
	{
		slider.value = value;
		breakReverse.SetActive(value < -0.3f);
		slider.gameObject.SetActive(value >= -0.3f);
	}
}
