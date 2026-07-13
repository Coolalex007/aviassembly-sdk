using System.Text.RegularExpressions;
using TMPro;
using UnityEngine;
using UnityEngine.InputSystem;

public class KeybindField : MonoBehaviour
{
	public TMP_Text keyName;

	public KeyIcon keyValue;

	public KeyIcon secondaryKeyValue;

	public string keyNameOverride;

	public Keys key;

	public AudioDef bindSound;

	[HideInInspector]
	public KeybindPanel keybindPanel;

	private InputActionRebindingExtensions.RebindingOperation rebindingOperation;

	private KeyIcon currentRebindText;

	private ControlScheme currentControlSceme;

	private void Start()
	{
		keyValue.SetValue(Singleton<InputManager>.Instance.GetKeyPath(key, ControlScheme.KeyboardAndMouse));
		secondaryKeyValue.SetValue(Singleton<InputManager>.Instance.GetKeyPath(key, ControlScheme.Gamepad));
		keyName.text = SplitCamelCase(string.IsNullOrWhiteSpace(keyNameOverride) ? key.ToString() : keyNameOverride);
	}

	private string SplitCamelCase(string source)
	{
		string[] array = Regex.Split(source, "(?<!^)(?=[A-Z])");
		string text = "";
		for (int i = 0; i < array.Length; i++)
		{
			text = text + array[i] + " ";
		}
		return text;
	}

	public void StartPrimaryKeyBinding()
	{
		keybindPanel.StartKeybind();
		rebindingOperation = Singleton<InputManager>.Instance.StartKeyRebind(key, ControlScheme.KeyboardAndMouse);
		keyValue.Wait();
		currentRebindText = keyValue;
		currentControlSceme = ControlScheme.KeyboardAndMouse;
	}

	public void StartSecondaryKeyBinding()
	{
		keybindPanel.StartKeybind();
		rebindingOperation = Singleton<InputManager>.Instance.StartKeyRebind(key, ControlScheme.Gamepad);
		secondaryKeyValue.Wait();
		currentRebindText = secondaryKeyValue;
		currentControlSceme = ControlScheme.Gamepad;
	}

	public void CancelRebinding()
	{
		if (rebindingOperation != null)
		{
			rebindingOperation.Cancel();
			rebindingOperation = null;
			if (keyValue != null && keyValue.text != null && Singleton<InputManager>.Instance != null)
			{
				currentRebindText.SetValue(Singleton<InputManager>.Instance.GetKeyPath(key, currentControlSceme));
			}
		}
	}

	private void Update()
	{
		if (rebindingOperation != null && rebindingOperation.completed)
		{
			Singleton<InputManager>.Instance.SaveKeybinds();
			Singleton<InputManager>.Instance.RefreshDisplayNames();
			Singleton<InputManager>.Instance.RefreshBindingPaths();
			currentRebindText.SetValue(Singleton<InputManager>.Instance.GetKeyPath(key, currentControlSceme));
			rebindingOperation = null;
			Singleton<AudioManager>.Instance.PlaySound(bindSound);
		}
		if (rebindingOperation != null && rebindingOperation.canceled)
		{
			currentRebindText.SetValue(Singleton<InputManager>.Instance.GetKeyPath(key, currentControlSceme));
			rebindingOperation = null;
		}
	}

	private void OnDestroy()
	{
		CancelRebinding();
	}
}
