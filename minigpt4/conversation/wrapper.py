from dataclasses import dataclass
from typing import List

from PIL import Image

from minigpt4.common.config import Config
from minigpt4.common.registry import registry
from minigpt4.conversation.conversation import Chat, CONV_VISION


@dataclass
class Argz:
    cfg_path: str = "eval_configs/minigpt4_eval.yaml"
    gpu_id: int = 0
    options: List[str] = None


class ChatWrapper:

    def __init__(
            self,
            num_beams: int = 1,
            temperature: float = 1.0,
    ):
        self.num_beams = num_beams
        self.temperature = temperature

        args = Argz()
        cfg = Config(args)

        model_config = cfg.model_cfg
        model_config.device_8bit = args.gpu_id
        model_cls = registry.get_model_class(model_config.arch)
        model = model_cls.from_config(model_config).to('cuda:{}'.format(args.gpu_id))

        vis_processor_cfg = cfg.datasets_cfg.cc_sbu_align.vis_processor.train
        vis_processor = registry.get_processor_class(vis_processor_cfg.name).from_config(vis_processor_cfg)
        self.chat = Chat(model, vis_processor, device='cuda:{}'.format(args.gpu_id))

        self.chat_state = None
        self.img_list = None

        print('Initialization Finished')

    def ask_about_image(self, image: Image, question: str):
        self.chat_state = CONV_VISION.copy()
        self.img_list = []
        self.chat.upload_img(image, self.chat_state, self.img_list)
        return self._do_ask(question)

    def follow_up(self, question: str):
        assert self.chat_state, "Call ask_about_image() first"
        return self._do_ask(question)

    def _do_ask(self, question):
        self.chat.ask(question, self.chat_state)
        answer = self.chat.answer(
            conv=self.chat_state,
            img_list=self.img_list,
            num_beams=self.num_beams,
            temperature=self.temperature,
            max_new_tokens=300,
            max_length=2000
        )
        return answer[0]
