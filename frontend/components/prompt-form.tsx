'use client'

import * as React from 'react'
import Textarea from 'react-textarea-autosize'
import { Button } from '@/components/ui/button'
import { IconArrowElbow, IconPlus } from '@/components/ui/icons'
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip'
import { useEnterSubmit } from '@/lib/hooks/use-enter-submit'
import { nanoid } from 'nanoid'
import { useRouter } from 'next/navigation'
import { useUIState } from 'ai/rsc'
import { UserMessage ,ChatMessage} from './stocks/message'
import { type AI } from '@/lib/chat/actions'

//======================
// Khai báo hàm createStreamableUI trực tiếp
type StreamableUIWrapper = {
  readonly value: React.ReactNode;
  update(value: React.ReactNode): StreamableUIWrapper;
  append(value: React.ReactNode): StreamableUIWrapper;
  error(error: any): StreamableUIWrapper;
  done(...args: [React.ReactNode] | []): StreamableUIWrapper;
};

// Giả sử hàm này được định nghĩa ở đâu đó
function createStreamableUI(initialValue?: React.ReactNode): StreamableUIWrapper {
  let currentValue = initialValue;
  return {
    get value() {
      return currentValue;
    },
    update(value: React.ReactNode) {
      currentValue = value;
      return this;
    },
    append(value: React.ReactNode) {
      currentValue = (
        <>
          {currentValue}
          {value}
        </>
      );
      return this;
    },
    error(error: any) {
      currentValue = <div>Error: {error.message}</div>;
      return this;
    },
    done(...args: [React.ReactNode] | []) {
      return this;
    },
  };
}
//======================

export function PromptForm({
  input,
  setInput
}: {
  input: string
  setInput: (value: string) => void
}) {
  const router = useRouter()
  const { formRef, onKeyDown } = useEnterSubmit()
  const inputRef = React.useRef<HTMLTextAreaElement>(null)
  const [_, setMessages] = useUIState<typeof AI>()
  const [stream, setStream] = React.useState<StreamableUIWrapper | null>(null)

  React.useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus()
    }
  }, [])

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()

    const value = input.trim()
    setInput('')
    if (!value) return

    // Optimistically add user message UI
    setMessages(currentMessages => [
      ...currentMessages,
      {
        id: nanoid(),
        display: <UserMessage>{value}</UserMessage>
      }
    ])

    // Initialize streamable UI
    const newStream = createStreamableUI();

    try {
      // Fetch response from the API
      const response = await fetch('http://10.0.65.166:9090/query', {
        method: 'POST',
        body: JSON.stringify({ message: value }),
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`Network response was not ok: ${response.statusText}`)
      }

      const reader = response.body?.getReader()
      const decoder = new TextDecoder()
      if (reader) {
        // Handle streaming response
        while (true) {
          const { done, value } = await reader.read()
          if (done) break
          const chunk = decoder.decode(value, { stream: true })
          newStream.append(chunk)
        }
        newStream.done('Streaming completed') // Mark stream as done
      }

      // Update the messages state with the streamed response
      setMessages(currentMessages => [
        ...currentMessages,
        {
          id: nanoid(),
          display: <ChatMessage>{newStream.value}</ChatMessage>
        }
      ])

    } catch (error) {
      console.error('Error fetching message:', error)
      // Optionally handle error (e.g., show error message to user)
      setMessages(currentMessages => [
        ...currentMessages,
        {
          id: nanoid(),
          display: <ChatMessage>Error fetching message.</ChatMessage>
        }
      ])
    }
  }

  return (
    <form ref={formRef} onSubmit={handleSubmit}>
      <div className="relative flex max-h-60 w-full grow flex-col overflow-hidden bg-background px-8 sm:rounded-md sm:border sm:px-12">
        <Tooltip>
          <TooltipTrigger asChild>
            <Button
              variant="outline"
              size="icon"
              className="absolute left-0 top-[14px] size-8 rounded-full bg-background p-0 sm:left-4"
              onClick={() => {
                router.push('/new')
              }}
            >
              <IconPlus />
              <span className="sr-only">New Chat</span>
            </Button>
          </TooltipTrigger>
          <TooltipContent>New Chat</TooltipContent>
        </Tooltip>
        <Textarea
          ref={inputRef}
          tabIndex={0}
          onKeyDown={onKeyDown}
          placeholder="Send a message."
          className="min-h-[60px] w-full resize-none bg-transparent px-4 py-[1.3rem] focus-within:outline-none sm:text-sm"
          autoFocus
          spellCheck={false}
          autoComplete="off"
          autoCorrect="off"
          name="message"
          rows={1}
          value={input}
          onChange={e => setInput(e.target.value)}
        />
        <div className="absolute right-0 top-[13px] sm:right-4">
          <Tooltip>
            <TooltipTrigger asChild>
              <Button type="submit" size="icon" disabled={input === ''}>
                <IconArrowElbow />
                <span className="sr-only">Send message</span>
              </Button>
            </TooltipTrigger>
            <TooltipContent>Send message</TooltipContent>
          </Tooltip>
        </div>
      </div>
    </form>
  )
}
