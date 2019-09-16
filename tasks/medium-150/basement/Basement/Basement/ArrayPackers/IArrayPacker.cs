using System;

namespace Basement
{
	public interface IArrayPacker<TUnpacked, TPacked>
	{
		TPacked[] Pack(TUnpacked[] array);
		TUnpacked[] Unpack(TPacked[] array);
	}
}
