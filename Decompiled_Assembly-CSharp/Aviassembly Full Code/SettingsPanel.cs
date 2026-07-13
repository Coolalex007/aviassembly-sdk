using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class SettingsPanel : MonoBehaviour
{
	public TMP_Dropdown resolutionDropdown;

	public Toggle fullscreenToggle;

	public Toggle autoSteerToggle;

	public Toggle autoSaveToggle;

	public Toggle vSync;

	public Toggle shadows;

	public Toggle SSAO;

	public Toggle antiAliassing;

	public Slider volumeSlider;

	public Slider musicVolumeSlider;

	public Slider drawDistance;

	public GameObject[] panels;

	public SettingsPanelHeaderButton[] buttons;

	public Color selectedButton;

	public Color deselectedButton;

	public Color selectedButtonShadow;

	public Color deselectedButtonShadow;

	public Color selectedIcon;

	public Color deselectedIcon;

	private BackgroundMusicManager backgroundMusicManager;

	private GameSettings gameSettings;

	private void Awake()
	{
		for (int i = 0; i < buttons.Length; i++)
		{
			buttons[i].settingsPanel = this;
			buttons[i].Init();
		}
		OpenPanel(0);
		backgroundMusicManager = Object.FindFirstObjectByType<BackgroundMusicManager>();
		gameSettings = new GameSettings();
		gameSettings.LoadSettings();
		if (GameManager.firstMenuOpen)
		{
			Singleton<GameManager>.Instance.unlockRaces = gameSettings.raceProgress;
		}
		volumeSlider.SetValueWithoutNotify(gameSettings.masterVolume);
		musicVolumeSlider.SetValueWithoutNotify(gameSettings.musicVolume);
		Screen.SetResolution(gameSettings.resolution.x, gameSettings.resolution.y, gameSettings.fullscreen);
		resolutionDropdown.ClearOptions();
		Resolution[] resolutions = Screen.resolutions;
		List<string> list = new List<string>();
		int valueWithoutNotify = 0;
		for (int j = 0; j < resolutions.Length; j++)
		{
			list.Add(resolutions[j].width + " x " + resolutions[j].height);
			if (gameSettings.resolution.x == resolutions[j].width && gameSettings.resolution.y == resolutions[j].height)
			{
				valueWithoutNotify = j;
			}
		}
		resolutionDropdown.AddOptions(list);
		resolutionDropdown.SetValueWithoutNotify(valueWithoutNotify);
		fullscreenToggle.SetIsOnWithoutNotify(gameSettings.fullscreen);
		Singleton<GameManager>.Instance.graphicsSettings.drawDistance = gameSettings.drawDistance;
		Singleton<GameManager>.Instance.graphicsSettings.targetDrawDistance = gameSettings.drawDistance;
		drawDistance.SetValueWithoutNotify(Mathf.InverseLerp(1000f, 4000f, Singleton<GameManager>.Instance.graphicsSettings.drawDistance));
		Update();
		Singleton<GameManager>.Instance.autoSteer = gameSettings.autoSteer;
		autoSteerToggle.SetIsOnWithoutNotify(Singleton<GameManager>.Instance.autoSteer);
		Singleton<GameManager>.Instance.autoSave = gameSettings.autoSave;
		autoSaveToggle.SetIsOnWithoutNotify(Singleton<GameManager>.Instance.autoSave);
		shadows.SetIsOnWithoutNotify(gameSettings.shadows);
		ToggleShadows(gameSettings.shadows);
		vSync.SetIsOnWithoutNotify(gameSettings.vSync);
		ToggleVSync(gameSettings.vSync);
		SSAO.SetIsOnWithoutNotify(gameSettings.ssao);
		ToggleSSAO(gameSettings.ssao);
		antiAliassing.SetIsOnWithoutNotify(gameSettings.antiAliasing);
		ToggleAntiAliasing(gameSettings.antiAliasing);
	}

	private void Update()
	{
		AudioListener.volume = volumeSlider.value;
		backgroundMusicManager.musicVolume = musicVolumeSlider.value;
		gameSettings.musicVolume = musicVolumeSlider.value;
		gameSettings.masterVolume = volumeSlider.value;
		Singleton<GameManager>.Instance.graphicsSettings.targetDrawDistance = Mathf.Lerp(1000f, 4000f, drawDistance.value);
		gameSettings.drawDistance = Mathf.Lerp(1000f, 4000f, drawDistance.value);
		gameSettings.raceProgress = Singleton<GameManager>.Instance.unlockRaces;
		gameSettings.SaveSettings();
	}

	public void ToggleFullscreen(bool value)
	{
		Screen.fullScreenMode = (value ? FullScreenMode.FullScreenWindow : FullScreenMode.Windowed);
		gameSettings.fullscreen = value;
	}

	public void ToggleShadows(bool value)
	{
		Singleton<GameManager>.Instance.graphicsSettings.shadows = value;
		gameSettings.shadows = value;
	}

	public void ToggleVSync(bool value)
	{
		Singleton<GameManager>.Instance.graphicsSettings.vSync = value;
		QualitySettings.vSyncCount = (value ? 1 : 0);
		gameSettings.vSync = value;
	}

	public void ToggleSSAO(bool value)
	{
		Singleton<GameManager>.Instance.graphicsSettings.SSAO = value;
		gameSettings.ssao = value;
	}

	public void ToggleAutoSteer(bool value)
	{
		gameSettings.autoSteer = value;
		Singleton<GameManager>.Instance.autoSteer = value;
	}

	public void ToggleAutoSave(bool value)
	{
		gameSettings.autoSave = value;
		Singleton<GameManager>.Instance.autoSave = value;
	}

	public void ToggleAntiAliasing(bool value)
	{
		QualitySettings.antiAliasing = (value ? 4 : 0);
		gameSettings.antiAliasing = value;
	}

	public void ChangeResolution(int index)
	{
		Vector2Int resolution = new Vector2Int(Screen.resolutions[index].width, Screen.resolutions[index].height);
		Screen.SetResolution(resolution.x, resolution.y, Screen.fullScreenMode);
		gameSettings.resolution = resolution;
	}

	public void OpenPanel(int index)
	{
		for (int i = 0; i < panels.Length; i++)
		{
			panels[i].gameObject.SetActive(index == i);
			buttons[i].SetColor((index == i) ? selectedButton : deselectedButton, (index == i) ? selectedIcon : deselectedIcon, (index == i) ? selectedButtonShadow : deselectedButtonShadow);
		}
	}

	public void Close()
	{
		base.gameObject.SetActive(value: false);
	}
}
