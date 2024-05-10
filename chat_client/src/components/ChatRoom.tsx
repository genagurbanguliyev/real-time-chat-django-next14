"use client"
import MessageList from "@/components/MessageList";
import ChatForm from "@/components/chatForm";
import {useEffect, useState, useCallback, useMemo, useRef} from "react";
import {MessageType, SendMessageType, UserInfoType} from "@/common.types";
import useWebSocket from "react-use-websocket";

import {encryptText} from "@/helper/encDecText"
import {getMessagesLongPolling, postMessagesLongPolling} from "@/server/api";

interface IChatRoom {
    userInfo: UserInfoType;
    recentMessages: MessageType[]
}

const ChatRoom: React.FC<IChatRoom> = ({ userInfo, recentMessages }) => {
    const messagesDiv = useRef<HTMLDivElement>(null);
    const [realtimeMessages, setRealtimeMessages] = useState<MessageType[]>([]);
    const [usingWebSockets, setUsingWebSockets] = useState(true);
    const [lastMessageId, setLastMessageId] = useState(realtimeMessages.length ? realtimeMessages[realtimeMessages.length-1].id : recentMessages.length ? recentMessages[recentMessages.length-1].id : 0);


    const poll = async () => {
                try {
                    const response = await getMessagesLongPolling(lastMessageId, userInfo);
                    if(response.ok && response.status === 200){
                        const data = await response.json();

                        setLastMessageId(data?.length && data[data.length - 1].id)
                        setRealtimeMessages((realtimeMessages) => [...realtimeMessages, ...data]);
                    }
                    // setRealtimeMessages((realtimeMessages) => [...realtimeMessages, data]);
                } catch (error) {
                    console.error('Long polling error:', error);
                }
            }

    const { sendJsonMessage,lastJsonMessage, readyState } = useWebSocket(`${process.env.NEXT_PUBLIC_WS_HOST}/ws/chat/?user_id=${userInfo.id}`, {
        share: false,
        shouldReconnect: () => true,
        reconnectAttempts: 2,
        reconnectInterval: 2000,
        onOpen: () => {
            console.log('opened');
        },
        onError: () => {
            console.log('Websocket connection error, and use Long Polling mechanism');
            setUsingWebSockets(false)
        }
      },
    )

    useEffect(() => {
        if(usingWebSockets) {
            if (lastJsonMessage && typeof lastJsonMessage === "object" && 'user' in lastJsonMessage && 'text' in lastJsonMessage && 'id' in lastJsonMessage && 'created_at' in lastJsonMessage) {
                const message: MessageType = {
                    id: lastJsonMessage.id as number,
                    user: lastJsonMessage.user as UserInfoType,
                    text: lastJsonMessage.text as string,
                    created_at: lastJsonMessage.created_at as Date,
                }
                setRealtimeMessages((realtimeMessages) => [...realtimeMessages, message]);
            }
        } else {
            // Long Polling logic
            const intervalId = setInterval(() => poll(), 5000); // Poll every 5 seconds
            return () => clearInterval(intervalId); // Clean up on component unmount
        }

        setTimeout(() => {
            scrollToBottom()
        }, 50);
    }, [lastJsonMessage, usingWebSockets, lastMessageId]);

    const sendMessage = useCallback(async (txt: string) => {
        console.log('sendMessage')
        // readyState == 0 ? setUsingWebSockets(false) : setUsingWebSockets(true)
        const sendText: string | null = encryptText(txt)
        console.log('------------', readyState)
        console.log('======================', usingWebSockets)
        if(sendText) {
            if (usingWebSockets) {
                sendJsonMessage({
                    event: 'chat_message',
                    data: {
                        text: sendText,
                    }
                });
            } else {
                try {
                    await postMessagesLongPolling(sendText, userInfo)
                } catch (error) {
                    console.log('sendMessage With Long POLLING:', error);
                }
            }

            setTimeout(() => {
                scrollToBottom()
            }, 50);
        }
    }, [readyState, usingWebSockets]);

     const scrollToBottom = () => {
        if (messagesDiv.current) {
            messagesDiv.current?.scrollIntoView({ behavior: 'smooth' })
        }
    }

    useEffect(() => {
        setRealtimeMessages(realtimeMessages.filter( (ele, ind) => ind === realtimeMessages.findIndex( elem => elem.id === ele.id && elem.id === ele.id)))
    }, [realtimeMessages.length]);

  return (
      <>
          <MessageList recentMessages={recentMessages} realtimeMessages={realtimeMessages} messagesDiv={messagesDiv} userInfo={userInfo} />
          <ChatForm sendMessage={sendMessage} />
      </>
  )
}

export default ChatRoom