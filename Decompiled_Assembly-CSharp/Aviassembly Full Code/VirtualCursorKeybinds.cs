using TMPro;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.UI;

public class VirtualCursorKeybinds : MonoBehaviour
{
	public TMP_Dropdown moveBind;

	public TMP_Dropdown zoomBind;

	public KeyIcon leftClickBind;

	public KeyIcon rightClickBind;

	public KeyIcon slowMoveBind;

	public Slider mouseSpeed;

	public Slider mouseSlowdown;

	private string[] padPaths;

	private InputActionRebindingExtensions.RebindingOperation rebindingOperation;

	private KeyIcon currentBinding;

	private void Start()
	{
		MouseInput instance = Singleton<MouseInput>.Instance;
		leftClickBind.SetValue(instance.leftButtonAction.bindings[0].effectivePath);
		rightClickBind.SetValue(instance.rightButtonAction.bindings[0].effectivePath);
		slowMoveBind.SetValue(instance.slowCursorAction.bindings[0].effectivePath);
		padPaths = new string[3];
		padPaths[0] = "<Gamepad>/leftStick";
		padPaths[1] = "<Gamepad>/rightStick";
		padPaths[2] = "<Gamepad>/dpad";
		mouseSpeed.SetValueWithoutNotify(instance.cursorSpeed / 2000f);
		mouseSlowdown.SetValueWithoutNotify(instance.mouseSlowdown);
		moveBind.SetValueWithoutNotify(GetValueFromString(instance.moveCursorAction.bindings[0].effectivePath));
		zoomBind.SetValueWithoutNotify(GetValueFromString(instance.zoomAction.bindings[0].effectivePath));
	}

	private int GetValueFromString(string value)
	{
		for (int i = 0; i < padPaths.Length; i++)
		{
			if (padPaths[i] == value)
			{
				return i;
			}
		}
		return 0;
	}

	public void Update()
	{
		MouseInput instance = Singleton<MouseInput>.Instance;
		instance.cursorSpeed = mouseSpeed.value * 2000f;
		instance.mouseSlowdown = mouseSlowdown.value;
		if (rebindingOperation != null)
		{
			currentBinding.Wait();
			if (rebindingOperation.completed || rebindingOperation.canceled)
			{
				currentBinding.SetValue(rebindingOperation.action.bindings[0].effectivePath);
				rebindingOperation = null;
			}
		}
		instance.SaveSettings();
	}

	public void MoveRebind(int value)
	{
		Singleton<MouseInput>.Instance.moveCursorAction.Disable();
		Singleton<MouseInput>.Instance.moveCursorAction.ApplyBindingOverride(padPaths[value]);
		Singleton<MouseInput>.Instance.moveCursorAction.Enable();
		Singleton<MouseInput>.Instance.SaveSettings();
	}

	public void ZoomRebind(int value)
	{
		Singleton<MouseInput>.Instance.zoomAction.ApplyBindingOverride(padPaths[value]);
		Singleton<MouseInput>.Instance.SaveSettings();
	}

	public void LeftClickRebind()
	{
		rebindingOperation = InputManager.RebindAction(Singleton<MouseInput>.Instance.leftButtonAction, 0);
		currentBinding = leftClickBind;
	}

	public void RightClickRebind()
	{
		rebindingOperation = InputManager.RebindAction(Singleton<MouseInput>.Instance.rightButtonAction, 0);
		currentBinding = rightClickBind;
	}

	public void SlowDownRebind()
	{
		rebindingOperation = InputManager.RebindAction(Singleton<MouseInput>.Instance.slowCursorAction, 0);
		currentBinding = slowMoveBind;
	}
}
