import { useField } from "formik";

import { FormInput } from "../ui";

export const FormikInput = ({ ...props }) => {
  const [field, meta] = useField(props);

  return <FormInput {...field} {...props} />;
}
