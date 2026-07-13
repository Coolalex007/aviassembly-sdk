using System.IO;

internal struct HistoryEntry(float money, MemoryStream plane)
{
	public float money = money;

	public MemoryStream plane = plane;
}
