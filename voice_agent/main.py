from dotenv import load_dotenv
load_dotenv()

from livekit import agents
from livekit.agents import AgentSession, AgentServer, JobContext, TurnHandlingOptions, inference, room_io
from livekit.plugins import noise_cancellation

from voice_agent.agent import ReceptionAgent

server = AgentServer()


@server.rtc_session(agent_name="reception-agent")
async def entrypoint(ctx: JobContext):
    session = AgentSession(
        stt="deepgram/nova-3:en",
        llm="openai/chat-latest",
        tts="cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
        turn_handling=TurnHandlingOptions(
            turn_detection=inference.TurnDetector(),
        ),
    )

    await session.start(
        agent=ReceptionAgent(),
        room=ctx.room,
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=noise_cancellation.BVC(),
            ),
        ),
    )

    await session.generate_reply(
        instructions="Greet the user and let them know you can answer their questions."
    )


if __name__ == "__main__":
    agents.cli.run_app(server)
