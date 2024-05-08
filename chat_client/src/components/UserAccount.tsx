import {getSession, logout} from "@/lib/actions";

export const UserAccount = async () => {
    const session = await getSession()
  return (
      <form action={async () => {
          "use server"
          await logout()
      }}>
          <button className="flex space-x-1" type="submit">
              {session && session?.user?.name != "" ? session?.user?.name : "User"}
          </button>
      </form>
  )
}
