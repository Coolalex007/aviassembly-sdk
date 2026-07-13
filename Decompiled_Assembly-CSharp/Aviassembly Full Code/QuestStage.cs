public struct QuestStage(string description, int stage)
{
	public string description = description;

	public int stage = stage;

	public static QuestStage NullStage()
	{
		return new QuestStage("", -1);
	}
}
