import {UserAccount} from "@/components/UserAccount";

const Header = () => {

  return (
      <nav className="bg-gray-600 sticky top-0 z-50 p-4 text-white">
          <div className="container mx-auto">
              <div className="flex justify-between items-center">
                  <span className="font-bold text-xl">GroupChat</span>
                    <UserAccount />
              </div>
          </div>
      </nav>
  )
}
export default Header