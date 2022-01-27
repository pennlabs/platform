import getCsrf from './csrf'

export const SITE_ORIGIN =
  process.env.NODE_ENV === 'production'
    ? `https://${process.env.DOMAIN || 'platform.pennlabs.org'}`
    : `http://localhost:${process.env.PORT || 3000}`

export function getApiUrl(path: string): string {
  if (/^https?:\/\//.test(path)) {
    const url = new URL(path)
    return url.pathname + url.search
  }
  return SITE_ORIGIN + path
}

export function doApiRequest(path: string, data?: any): Promise<Response> {
  let formattedData = data
  if (!formattedData) {
    formattedData = {}
  }
  formattedData.credentials = 'include'
  formattedData.mode = 'same-origin'
  if (typeof document !== 'undefined') {
    formattedData.headers = formattedData.headers || {}
    if (!(formattedData.body instanceof FormData)) {
      formattedData.headers.Accept = 'application/json'
      formattedData.headers['Content-Type'] = 'application/json'
    }
    formattedData.headers['X-CSRFToken'] = getCsrf()
  }
  if (formattedData.body && !(formattedData.body instanceof FormData)) {
    formattedData.body = JSON.stringify(formattedData.body)
  }
  return fetch(getApiUrl(path), formattedData)
}

interface Success {
  data: any
  success: true
}

interface Failure {
  success: false
}

type VerifiedResponse = Success | Failure

// wraps doApiRequest to return a discriminated union
// this allows us to distinguish between an error due to
// accessing incorrect resources or an internet issue

export async function doSuccessRequest(
  path: string,
  data?: any
): Promise<VerifiedResponse> {
  const res = await doApiRequest(path, data)
  if (!res.ok) {
    return {
      success: false,
    }
  }
  return {
    success: true,
    data: await res.json(),
  }
}

interface SuccessRequest {
  path: string
  data?: any
}

export async function doMultipleSuccessRequests(
  reqs: SuccessRequest[]
): Promise<VerifiedResponse> {
  const res = await Promise.all(
    reqs.map((req) => doSuccessRequest(req.path, req.data))
  )
  if (res.reduce((acc, curr) => acc && curr.success, true)) {
    return {
      success: true,
      // data-flow analysis isn't good enough to figure out
      // reduce condition makes sure all responses have succeeded
      data: res.map((succ) => (succ as Success).data),
    }
  } else {
    return {
      success: false,
    }
  }
}
