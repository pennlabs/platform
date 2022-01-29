import { useResourceList } from '@pennlabs/rest-hooks'
import React, { useMemo } from 'react'
import { Form } from 'react-bulma-components'
import { Control, Controller } from 'react-hook-form'
import Select from 'react-select'

interface DataOption {
  id: number
  name: string
}

export interface MultiSelectProps {
  control: Control
  route: string
  name: string
  disabled?: boolean
}

const toSelectOptions = (options: DataOption[]) =>
  options.map((obj) => ({ value: obj.id, label: obj.name }))

const MultiSelectInput = (props: MultiSelectProps) => {
  const { control, name, route, disabled } = props
  const { data: rawData } = useResourceList<DataOption>(
    route,
    (id) => `${route}${id}/`
  )

  const data = useMemo(() => rawData || [], [rawData])
  const selectOptions = useMemo(() => toSelectOptions(data), [data])

  return (
    <Controller
      name={name}
      control={control}
      render={({ field, fieldState: { error } }) => {
        const fieldValue = field.value || []
        return (
          <>
            <Select
              instanceId={`select-${name}`}
              isMulti
              {...field}
              // @ts-ignore
              value={fieldValue.map(({ id }) =>
                selectOptions.find(({ value }) => value === id)
              )}
              onChange={(evt) => {
                field.onChange(
                  evt.map(({ value }) => data.find(({ id }) => id === value))
                )
              }}
              options={selectOptions}
              isDisabled={disabled}
            />
            <Form.Help color="danger">{error ? error.message : ''}</Form.Help>
          </>
        )
      }}
    />
  )
}

export default MultiSelectInput
