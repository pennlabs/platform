/* eslint-disable camelcase */
import { mutateResourceFunction } from '@pennlabs/rest-hooks/dist/types'
import { HTMLInputTypeAttribute, useMemo } from 'react'
import { Button, Form } from 'react-bulma-components'
import { Control, Controller, useForm, useFormState } from 'react-hook-form'
import toast from 'react-hot-toast'
import { User } from '../../../types'
import MultiSelectInput from './multi-select'

export interface GenericInfoProps {
  mutate: mutateResourceFunction<User>
  initialData?: User
}

interface TextInputProps {
  control: Control
  disabled?: boolean
  name: string
  displayName: string
  type?: HTMLInputTypeAttribute
  rules: any
}

const TextInput = ({
  control,
  disabled,
  name,
  displayName,
  type = 'text',
  rules = { required: { value: true, message: 'Required field!' } },
}: TextInputProps) => (
  <Form.Field>
    <Form.Label>{displayName}</Form.Label>
    <Controller
      control={control}
      render={({ field, fieldState: { error } }) => (
        <>
          <Form.Input
            {...field}
            ref={null}
            // @ts-ignore
            domRef={field.ref}
            type={type}
            color={error ? 'danger' : 'black'}
            disabled={disabled}
          />
          <Form.Help color="danger">{error?.message || ''}</Form.Help>
        </>
      )}
      name={name}
      rules={rules}
    />
  </Form.Field>
)

const getGradYearLimits = () => {
  const year = new Date().getFullYear()
  return [year, year + 10]
}

const GenericInfoForm = ({ mutate, initialData }: GenericInfoProps) => {
  const { handleSubmit, control, reset } = useForm({
    defaultValues: initialData,
  })

  const { isDirty, isValid, isSubmitting } = useFormState({ control })
  const canSubmit = isDirty && isValid && !isSubmitting

  const [minGradYear, maxGradYear] = useMemo(getGradYearLimits, [])

  const onSubmit = async (formData: Partial<User>) => {
    const { first_name, student } = formData
    // once we have error handling we can actually make this work...
    // console.log(formData)
    await toast.promise(
      mutate({
        first_name,
        student: student || { graduation_year: null, major: [], school: [] },
      }),
      {
        loading: 'Saving...',
        success: 'Saved!',
        error: 'Something went wrong...',
      }
    )
    reset(await mutate())
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <TextInput
        // @ts-ignore
        control={control}
        name="first_name"
        displayName="Display Name"
        disabled={isSubmitting}
      />
      {initialData?.student && (
        <>
          <Form.Field>
            <Form.Label>Majors</Form.Label>
            <MultiSelectInput
              route="/accounts/majors/"
              // @ts-ignore
              control={control}
              name="student.major"
              disabled={isSubmitting}
            />
          </Form.Field>
          <Form.Field>
            <Form.Label>Schools</Form.Label>
            <MultiSelectInput
              route="/accounts/schools/"
              // @ts-ignore
              control={control}
              name="student.school"
              disabled={isSubmitting}
            />
          </Form.Field>
          <TextInput
            // @ts-ignore
            control={control}
            name="student.graduation_year"
            displayName="Graduation Year"
            rules={{
              min: { value: minGradYear, message: 'Invalid grad year!' },
              max: { value: maxGradYear, message: 'Invalid grad year!' },
            }}
            type="number"
            disabled={isSubmitting}
          />
        </>
      )}
      <Form.Control>
        <Button type="submit" color="primary" disabled={!canSubmit}>
          Save
        </Button>
      </Form.Control>
    </form>
  )
}

export default GenericInfoForm
