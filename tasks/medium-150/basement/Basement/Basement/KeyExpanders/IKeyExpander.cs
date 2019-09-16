using System;

namespace Basement
{
	public interface IKeyExpander<T>
	{
		T[] Expand(T key, int length);
	}
}
