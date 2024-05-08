
// import { NextRequest } from "next/server";
// import { updateSession } from "@/lib/actions";
//
// export async function middleware(request: NextRequest) {
//   console.log("req======= ",request)
//   return await updateSession(request);
// }

import { NextRequest, NextResponse } from 'next/server'
import {getSession} from '@/lib/actions'

// 1. Specify protected and public routes
const privateRoutes = ['/chatgroup']
const publicRoutes = ['/login']

export default async function middleware(req: NextRequest) {
  const path = req.nextUrl.pathname
  if(path == '/') return NextResponse.redirect(new URL('/chatgroup', req.nextUrl))

  const isPrivateRoutes = privateRoutes.includes(path)
  const isPublicRoute = publicRoutes.includes(path)

  const session = await getSession()

  if (isPrivateRoutes && !session?.user?.id) return NextResponse.redirect(new URL('/login', req.nextUrl))
  if ( isPublicRoute && session?.user?.id ) return NextResponse.redirect(new URL('/chatgroup', req.nextUrl))
  return NextResponse.next()
}

// export const config = {
//   matcher: '/',
// }
// Routes Middleware should not run on
export const config = {
  matcher: ['/((?!api|_next/static|_next/image|.*\\.png$).*)'],
}