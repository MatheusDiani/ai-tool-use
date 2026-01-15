import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from src.agent import create_agent


def main():
    try:
        agent = create_agent()
    except Exception as e:
        print(f"❌ Erro: {e}")
        return
    
    while True:
        try:
            user_input = input("\n👤 Você: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ["sair", "exit", "quit"]:
                print("👋 Até logo!")
                break
            
            response = agent.run(user_input)
            print(f"\n🤖 Assistente: {response}")
            
        except KeyboardInterrupt:
            print("\n👋 Até logo!")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")


if __name__ == "__main__":
    main()
