import {Suspense} from "react";

import dynamic from 'next/dynamic'
import {getSession} from "@/lib/actions";
import {MessageType, SessionType, UserInfoType} from "@/common.types";

import {redirect} from "next/navigation";
import {getMessages} from "@/server/api";
const ChatRoom = dynamic(() => import('@/components/ChatRoom'), { ssr: false })

export default async function Page() {
    const session: SessionType = await getSession()
    if(!session || !session?.user?.id) { redirect("/login"); return; }
    const userInfo: UserInfoType = session?.user
    const res = await getMessages(userInfo)
    let recentMessages: MessageType[] = []
    if (res.ok) {
      recentMessages = await res.json()
    } else {
      console.log("ERR = ",res);
    }

  return (
      <Suspense fallback={<p>loading...</p>}>
        <ChatRoom userInfo={userInfo} recentMessages={recentMessages} />
      </Suspense>
  )
}