import {UserInfoType} from "@/common.types";

export async function getMessages(userInfo: UserInfoType) {
  return await fetch(`${process.env.NEXT_PUBLIC_SERVER_BASE}/api/v1/messages`,{
        // mode: 'no-cors',
        method: 'GET',
        headers: {
          "Content-Type": "application/json",
            // "Access-Control-Allow-Origin": "*",
            // "Access-Control-Allow-Headers": "*",
            'User': userInfo.id
        }
  })
}

export async function getMessagesLongPolling(lastMessageId: number, userInfo: UserInfoType) {
    return await fetch(`${process.env.NEXT_PUBLIC_SERVER_BASE}/api/v1/messages/long-polling?last_message_id=${lastMessageId}`, {
        // mode: 'no-cors',
        method: 'GET',
        headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            'User': userInfo.id
        }
    })
}

export async function postMessagesLongPolling(txt: string, userInfo: UserInfoType) {
  return await fetch(`${process.env.NEXT_PUBLIC_SERVER_BASE}/api/v1/messages/long-polling`,{
        method: 'POST',
        headers: {
          "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            'User': userInfo.id
        },
        body: JSON.stringify({
            data: {
                text: txt,
            }
        })
  })
}