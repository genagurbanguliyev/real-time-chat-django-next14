import {getSession, logout} from "@/lib/actions";

export const UserAccount = async () => {
    const session = await getSession()
  return (
    <div className="flex">
        <div>
              {session && session?.user?.name != "" ? session?.user?.name : "User"}
          </div>
          <span className="mx-3">|</span> 
      <form action={async () => {
          "use server"
          await logout()
      }}>
          <button type="submit">
              OUT
          </button>
      </form>
    </div>
  )
}
