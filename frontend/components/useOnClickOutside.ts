import { useEffect, useRef } from "react";

export function useOnClickOutside(onClickOutside: () => void, disabled: boolean) {
  const ref = useRef<HTMLElement>();

  useEffect(() => {
    const checkClickOutside = (e) => {
      if (ref.current && !ref.current.contains(e.target)) {
        onClickOutside();
      }
    };
    if (!disabled) {
      window.addEventListener("click", checkClickOutside);
      return () => {
        window.removeEventListener("click", checkClickOutside);
      };
    }
  }, [disabled, onClickOutside]);

  return ref;
}
