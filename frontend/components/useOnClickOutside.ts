import { useEffect, useRef } from 'react'

export function useOnClickOutside(
  onClickOutside: () => void,
  disabled: boolean
) {
  const ref = useRef<HTMLElement>()

  useEffect(() => {
    const checkClickOutside = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        onClickOutside()
      }
    }
    if (!disabled) {
      window.addEventListener('mousedown', checkClickOutside)
      return () => {
        window.removeEventListener('mousedown', checkClickOutside)
      }
    }
    return () => {}
  }, [disabled, onClickOutside])

  return ref
}
