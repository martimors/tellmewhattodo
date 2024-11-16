import { describe, it, expect } from 'vitest'

import { mount } from '@vue/test-utils'
import AlertItem from '../AlertItem.vue'

describe('HelloWorld', () => {
  it('renders properly', () => {
    const wrapper = mount(AlertItem, {
      props: {
        id: '5',
        created_at: new Date(),
        description: 'Hello Vitest',
        acked: false,
        name: 'Hello Vitest',
        alert_type: 'foobar',
      },
    })
    expect(wrapper.text()).toContain('Hello Vitest')
  })
})
