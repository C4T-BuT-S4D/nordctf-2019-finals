using System;

namespace Basement
{
	public interface IBytesCoder
	{
		byte[] Encode(byte[] bytes, int times = 1);
		byte[] Decode(byte[] bytes, int times = 1);
	}
}
