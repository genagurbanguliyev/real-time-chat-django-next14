"use client"
import MessageList from "@/components/MessageList";
import ChatForm from "@/components/chatForm";
import {useEffect, useState, useCallback, useMemo, useRef} from "react";
import {MessageType, UserInfoType} from "@/common.types";
import useWebSocket from "react-use-websocket";

interface IChatRoom {
    userInfo: UserInfoType;
    recentMessages: MessageType[]
}

const ChatRoom: React.FC<IChatRoom> = ({ userInfo, recentMessages }) => {
    const messagesDiv = useRef<HTMLDivElement>(null);
    // const [recentMessages, setRecentMessages] = useState<MessageType[]>([]);
    const [realtimeMessages, setRealtimeMessages] = useState<MessageType[]>([]);


    const { sendJsonMessage,lastJsonMessage, readyState, getWebSocket } = useWebSocket(`${process.env.NEXT_PUBLIC_WS_HOST}/ws/chat/?user_id=${userInfo.id}`, {
        share: false,
        shouldReconnect: () => true,
        reconnectAttempts: 3,
        reconnectInterval: 2000,
        onOpen: () => console.log('opened'),
        onError: () => alert('Socket cannot connect')
      },
    )


    useEffect(() => {
        if (lastJsonMessage && typeof lastJsonMessage === "object" &&  'user' in lastJsonMessage && 'text' in lastJsonMessage) {
            const message: MessageType = {
                user: lastJsonMessage.user as UserInfoType,
                text: lastJsonMessage.text as string,
            }

            setRealtimeMessages((realtimeMessages) => [...realtimeMessages, message]);
        }

        setTimeout(() => {
            scrollToBottom()
        }, 50);
    }, [lastJsonMessage]);

    const sendMessage = useCallback((txt: string) => {
        console.log('sendMessage')
        sendJsonMessage({
            event: 'chat_message',
            data: {
                text: txt,
            }
        });

        setTimeout(() => {
            scrollToBottom()
        }, 50);
    }, []);

     const scrollToBottom = () => {
        if (messagesDiv.current) {
            messagesDiv.current?.scrollIntoView({ behavior: 'smooth' })
        }
    }

  return (
      <>
          <MessageList recentMessages={recentMessages} realtimeMessages={realtimeMessages} messagesDiv={messagesDiv} userInfo={userInfo} />
          <ChatForm sendMessage={sendMessage} />
      </>
  )
}

export default ChatRoom