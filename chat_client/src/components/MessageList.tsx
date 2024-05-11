"use client"
import Message from '@/components/Message'
import {MessageType, UserInfoType} from "@/common.types";
import {LegacyRef} from "react";

interface IMessageList {
  recentMessages: MessageType[],
  realtimeMessages: MessageType[],
  userInfo: UserInfoType
  messagesDiv: LegacyRef<HTMLDivElement>
}

const MessageList: React.FC<IMessageList> = ({recentMessages, realtimeMessages, messagesDiv, userInfo}) => {
  return (
    <div className="flex flex-col space-y-3 overflow-y-hidden">
      {
        recentMessages?.length && recentMessages.map((node: MessageType, index: number) => (
              <Message key={index} message={node} userInfo={userInfo} />
        ))
      }{
        realtimeMessages?.length &&  realtimeMessages.map((node: MessageType, index: number) => (
              <Message key={index} message={node} userInfo={userInfo} />
        ))
      }
      <div ref={messagesDiv} style={{ height: "50px"}}></div>
    </div>
  )
}

export default MessageList