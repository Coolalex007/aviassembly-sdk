using TMPro;
using UnityEngine.InputSystem;

public class DecoupleSettings : PartSettingsBase
{
	public TMP_Text rebindText;

	private Decoupler decoupler;

	private InputActionRebindingExtensions.RebindingOperation rebinding;

	private void Update()
	{
		rebindText.text = decoupler.inputOverride.bindings[0].ToDisplayString();
		if (rebinding != null)
		{
			rebindText.text = "-";
			if (rebinding.completed || rebinding.canceled)
			{
				rebinding = null;
			}
		}
	}

	public void CancelRebind()
	{
		if (rebinding != null)
		{
			rebinding.Cancel();
			rebinding = null;
		}
	}

	public void StartForwardOverride()
	{
		rebinding = InputManager.RebindAction(decoupler.inputOverride, 0);
	}

	public override void SelectPart(PlanePart part)
	{
		decoupler = (Decoupler)part;
		rebindText.text = decoupler.inputOverride.bindings[0].ToDisplayString();
	}

	private void OnDisable()
	{
		CancelRebind();
	}
}
