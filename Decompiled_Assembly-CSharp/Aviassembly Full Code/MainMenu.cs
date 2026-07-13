using UnityEngine;

public class MainMenu : MonoBehaviour
{
	[Header("Menus")]
	public GameObject mainMenu;

	public GameObject playGameMenu;

	[Header("Panels")]
	public GameObject loadPanel;

	public GameObject demoQuitPanel;

	private void Start()
	{
		OpenObject(mainMenu);
	}

	public void OpenObject(GameObject gameObject)
	{
		loadPanel.SetActive(value: false);
		playGameMenu.SetActive(value: false);
		mainMenu.SetActive(value: false);
		if (gameObject != null)
		{
			gameObject.SetActive(value: true);
		}
	}

	public void OpenNewGameMenu()
	{
		OpenObject(playGameMenu);
	}

	public void OpenMainMenu()
	{
		OpenObject(mainMenu);
	}

	public void StartNewGame()
	{
		Singleton<GameManager>.Instance.currentSaveFile = "";
		Singleton<GameManager>.Instance.gameModeData.creativeMode = false;
		Singleton<GameManager>.Instance.gameModeData.disableAirports = false;
		Singleton<GameManager>.Instance.gameModeData.unlockAll = false;
		Singleton<GameManager>.Instance.StartGame();
	}

	public void QuitGame()
	{
		Application.Quit();
	}

	public void InitQuit()
	{
		QuitGame();
	}

	public void StartCreativeMode()
	{
		Singleton<GameManager>.Instance.currentSaveFile = "";
		Singleton<GameManager>.Instance.gameModeData.creativeMode = true;
		Singleton<GameManager>.Instance.gameModeData.unlockAll = true;
		Singleton<GameManager>.Instance.gameModeData.disableAirports = true;
		Singleton<GameManager>.Instance.StartGame();
	}

	public void StartRace()
	{
		Singleton<GameManager>.Instance.currentSaveFile = "";
		Singleton<GameManager>.Instance.gameModeData.creativeMode = false;
		Singleton<GameManager>.Instance.gameModeData.unlockAll = true;
		Singleton<GameManager>.Instance.gameModeData.disableAirports = true;
		Singleton<GameManager>.Instance.StartGame();
	}

	public void SetMapType(int index)
	{
		Singleton<GameManager>.Instance.gameModeData.mapType = (MapType)index;
	}
}
