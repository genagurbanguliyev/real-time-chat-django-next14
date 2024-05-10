export type SessionType = {
    user: UserInfoType,
    expires: Date,
    iat: string | number,
    exp: string | number
}

export type UserInfoType = {
    id: string,
    name: string | null
}

export type MessageType = {
    id: number,
    user: UserInfoType,
    text: string,
    created_at: Date,
}

export type SendMessageType = {
    user: UserInfoType,
    text: string
}
