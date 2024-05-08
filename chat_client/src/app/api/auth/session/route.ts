import {cookies} from "next/headers";
import {decrypt} from "@/lib/actions";
import {NextResponse} from "next/server";

export async function GET(
  req: Request,
) {
    try {
      const session = cookies().get("session")?.value;
      if (!session) return null;
      const data = await decrypt(session);
      console.log("API route data route: ", data);
      return  NextResponse.json(data)
    } catch (err) {
      return  NextResponse.json({error: 'failed to load data'})
    }
}
// export async function POST(
//   req: Request,
// ) {
//     try {
//       const session = cookies().get("session")?.value;
//       if (!session) return null;
//       const data = await decrypt(session);
//       console.log("API route data route: ", data);
//       return  NextResponse.json(data)
//     } catch (err) {
//       return  NextResponse.json({error: 'failed to load data'})
//     }
// }