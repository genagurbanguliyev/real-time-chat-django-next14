'use client'
import {useState} from "react";

interface UserMessage {
    sendMessage: (txt: string) => void,
}

const ChatForm: React.FC<UserMessage> = ({
    sendMessage,
}) => {
    const [ newMessage, setNewMessage ] = useState("")

    const handleSend = () => {
        if (newMessage) {
            try{
                sendMessage(newMessage)
                setNewMessage("")
            } catch (error) {
                console.error("Send msg callback error: ",error)
            }
        }
    }

    return (
        <div className="bg-gray-600 sticky bottom-0 z-50 p-4 text-white">
          <div className="container mx-auto flex items-center space-x-3">
                  <input
                      autoFocus
                      id="newMessage"
                      name="newMessage"
                      placeholder="Write a newMessage..."
                      value={newMessage}
                      onChange={e => setNewMessage(e.target.value)}
                      className="flex-1 h-12 px-3 rounded bg-[#222226] border border-[#222226] focus:border-[#222226] focus:outline-none text-white placeholder-white"
                  />
                  <button
                      type="button"
                      className="bg-[#222226] rounded h-12 font-medium text-white w-24 text-lg border border-transparent"
                      disabled={!newMessage}
                      onClick={handleSend}
                  >
                      Send
                  </button>
              </div>
      </div>
    )
}

export default ChatForm