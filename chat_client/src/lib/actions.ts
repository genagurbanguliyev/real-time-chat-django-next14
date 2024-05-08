import { SignJWT, jwtVerify } from "jose";
import { cookies } from "next/headers";
import {redirect} from "next/navigation";
import {NextRequest, NextResponse} from "next/server";
import {SessionType} from "@/common.types";

const secretKey = "secret";
const key = new TextEncoder().encode(secretKey);

export async function encrypt(payload: any) {
  return await new SignJWT(payload)
    .setProtectedHeader({ alg: "HS256" })
    .setIssuedAt()
    .setExpirationTime(payload.expires)
    .sign(key);
}

export async function decrypt(input: string | undefined): Promise<any> {
  if(input === undefined) return null
  const { payload } = await jwtVerify(input, key, {
    algorithms: ["HS256"],
  });
  return payload;
}

export async function login(formData: FormData) {
  const user = { name: formData.get("name") || 'User' };

  const res = await fetch(`${process.env.NEXT_PUBLIC_SERVER_BASE}/api/v1/check-user`,{
        method: 'POST',
        body: JSON.stringify(user),
        headers: {
          'content-type': 'application/json'
        }
  }
  )
    if (res.ok) {
      const user = await res.json()

      // Create the session
      const expires = new Date(Date.now() + 60 * 60 * 1000);
      const session = await encrypt({ user, expires });

      // Save the session in a cookie
      cookies().set("session", session, { expires, httpOnly: true });
      redirect("/chatgroup");
    } else {
      console.log("ERR = ",res);
    }
}

export async function logout() {
  cookies().set("session", "", { expires: new Date(0) });
  redirect("/login")
}

export async function getSession(): Promise<any> {
  const session = cookies().get("session")?.value;
  if (!session) return null;
  return await decrypt(session);
}

export async function updateSession(request: NextRequest) {
  const session = request.cookies.get("session")?.value;
  if (!session) return;

  // Refresh the session so it doesn't expire
  const parsed: SessionType = await decrypt(session);
  parsed.expires = new Date(Date.now() + 60 * 60 * 1000);
  const res = NextResponse.next();
  res.cookies.set({
    name: "session",
    value: await encrypt(parsed),
    httpOnly: true,
    expires: parsed.expires,
  });
  return res;
}