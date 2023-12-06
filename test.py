from waifuc.export import TextualInversionExporter
from waifuc.source import DanbooruSource, PixivSearchSource, ZerochanSource, LocalSource, GcharAutoSource
from waifuc.action import HeadCountAction, AlignMinSizeAction, CCIPAction, ThreeStageSplitAction, ModeConvertAction, ClassFilterAction, PersonSplitAction, TaggingAction, RatingFilterAction, NoMonochromeAction, RandomFilenameAction
from typing import Literal, cast


def download_images(source_type, character_name, p_min_size, p_background, p_class, p_rating, num_images):
    actions = []
    rating_map = {0: 'safe', 1: 'r15', 2: 'r18'}
    class_map = {1: 'illustration', 2: 'bangumi'}
    ratings_to_filter = set(rating_map.values()) - set([rating_map[i] for i in p_rating if i in rating_map])
    print("\n - start")
    character_list = character_name.split(',')
    for character in character_list:
        character = character.replace(' ', '_')
        save_path = 'dataset/' + character
        if source_type == 'Danbooru':
            source_init = DanbooruSource([character, 'solo'])
        else:
            pass
        if p_class:
            if 0 in p_class:
                actions.append(NoMonochromeAction())
            class_to_filter = set([class_map[i] for i in p_class if i in class_map])
            actions.append(ClassFilterAction(cast(list[Literal['illustration', 2: 'bangumi']], list(class_to_filter))))
        if p_min_size:
            actions.append(AlignMinSizeAction(min_size=int(p_min_size)))
        actions.append(ModeConvertAction('RGB', p_background))
        actions.append(HeadCountAction(1))
        actions.append(RandomFilenameAction(ext='.png'))
        actions.append(RatingFilterAction(ratings=cast(list[Literal['safe', 'r15', 'r18']], list(ratings_to_filter))))
        source_init.attach(*actions)[:int(num_images)].export(
            TextualInversionExporter(save_path)
        )
    return "string"


if __name__ == "__main__":
    download_images("Danbooru", "sex", "1024", "#FFFFFF", None, [0, 1, 2], 1000)
