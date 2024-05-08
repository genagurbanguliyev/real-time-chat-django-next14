import {MessageType, UserInfoType} from "@/common.types";
import {getSession} from "@/lib/actions";

export async function getMessages() {
    const userInfo: UserInfoType = await getSession()

  return await fetch(`${process.env.NEXT_PUBLIC_SERVER_BASE}/api/v1/messages`,{
        method: 'GET',
        headers: {
          'content-type': 'application/json',
            'User': userInfo.id
        }
  }
  )
}