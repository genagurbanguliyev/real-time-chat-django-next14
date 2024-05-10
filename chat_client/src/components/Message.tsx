'use client'

import {MessageType, UserInfoType} from "@/common.types";
import {decryptText} from "@/helper/encDecText";

interface IMessage {
  message: MessageType,
  userInfo: UserInfoType
}

const Message: React.FC<IMessage>= ({ message, userInfo }) => {

  return (
    <div
      className={`flex relative space-x-1 ${
        message.user.name === userInfo.name
          ? 'flex-row-reverse space-x-reverse'
          : 'flex-row'
      }`}
    >
      <div
        className={`rounded space-x-2 items-start p-3 text-white ${
          message.user.name === userInfo.name
            ? 'bg-[#4a9c6d]'
            : 'bg-[#363739]'
        } `}
      >
        {message.user.name !== userInfo.name && <p className="font-bold">{message.user.name !== "" ? message.user.name : message?.id}:</p> }
        <p>{decryptText(message?.text)}</p>
        {message?.created_at && <p className="font-thin">{String(new Date(message.created_at).toLocaleString())}</p>}
      </div>
    </div>
  )
}

export default Message