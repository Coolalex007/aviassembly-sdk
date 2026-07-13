using UnityEngine;

public class KeybindPanel : MonoBehaviour
{
	private KeybindField[] keybindFields;

	private void Awake()
	{
		keybindFields = GetComponentsInChildren<KeybindField>(includeInactive: true);
		for (int i = 0; i < keybindFields.Length; i++)
		{
			keybindFields[i].keybindPanel = this;
		}
	}

	public void StartKeybind()
	{
		for (int i = 0; i < keybindFields.Length; i++)
		{
			keybindFields[i].CancelRebinding();
		}
	}

	public void Open()
	{
		base.gameObject.SetActive(value: true);
	}

	public void Close()
	{
		for (int i = 0; i < keybindFields.Length; i++)
		{
			keybindFields[i].CancelRebinding();
		}
		base.gameObject.SetActive(value: false);
	}
}
