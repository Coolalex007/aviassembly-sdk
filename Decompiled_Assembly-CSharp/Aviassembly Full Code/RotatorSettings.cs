using TMPro;
using UnityEngine.InputSystem;

public class RotatorSettings : PartSettingsBase
{
	public TMP_Text backwardRebindText;

	public TMP_Text forwardRebindText;

	private Rotator rotator;

	private InputActionRebindingExtensions.RebindingOperation forwaredRebinding;

	private InputActionRebindingExtensions.RebindingOperation backwardRebinding;

	private void Update()
	{
		forwardRebindText.text = rotator.inputOverride.bindings[2].ToDisplayString();
		backwardRebindText.text = rotator.inputOverride.bindings[1].ToDisplayString();
		if (forwaredRebinding != null)
		{
			forwardRebindText.text = "-";
			if (forwaredRebinding.completed || forwaredRebinding.canceled)
			{
				forwaredRebinding = null;
			}
		}
		if (backwardRebinding != null)
		{
			backwardRebindText.text = "-";
			if (backwardRebinding.completed || backwardRebinding.canceled)
			{
				backwardRebinding = null;
			}
		}
	}

	public void CancelRebind()
	{
		if (forwaredRebinding != null)
		{
			forwaredRebinding.Cancel();
			forwaredRebinding = null;
		}
		if (backwardRebinding != null)
		{
			backwardRebinding.Cancel();
			backwardRebinding = null;
		}
	}

	public void StartForwardOverride()
	{
		backwardRebinding = InputManager.RebindAction(rotator.inputOverride, 1);
	}

	public void StartBackwardOverride()
	{
		forwaredRebinding = InputManager.RebindAction(rotator.inputOverride, 2);
	}

	public override void SelectPart(PlanePart part)
	{
		rotator = (Rotator)part;
		forwardRebindText.text = rotator.inputOverride.bindings[2].ToDisplayString();
		backwardRebindText.text = rotator.inputOverride.bindings[1].ToDisplayString();
	}

	private void OnDisable()
	{
		CancelRebind();
	}
}
