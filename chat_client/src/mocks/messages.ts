import {MessageType} from "@/common.types";

function generateMockMessages(length: number = 30): MessageType[] {
  const messages: MessageType[] = [];
  const names = ['gena', 'ben', 'alice', 'max', 'mia', 'leo', 'olivia', 'noah', 'emma', 'ava'];

  for (let i = 0; i < length; i++) {
    const name = Math.random() < 0.2 ? null : names[Math.floor(Math.random() * names.length)]; // 20% chance of null username
    const text = `This is a mock message ${i + 1}`;
    messages.push({
      id: (i + 1).toString(),
      user: {
        id: String(i),
        name: name
      },
      text,
      created_at: new Date()
    });
  }

  return messages;
}

export const mockMessages = generateMockMessages();

// messages: MessageSchema: [
//     {
//         id: '1',
//         username: 'gena',
//         text: 'hello',
//     }
// ]