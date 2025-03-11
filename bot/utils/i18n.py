from fluent_compiler.bundle import FluentBundle

from fluentogram import FluentTranslator, TranslatorHub


def create_translator_hub() -> TranslatorHub:
    translator_hub = TranslatorHub(
        {"ru": ("ru", "en", "uz"), "en": ("en", "ru", "uz"), "uz": ("uz", "en", "ru")},
        [
            FluentTranslator(
                locale="ru",
                translator=FluentBundle.from_files(
                    locale="ru-RU", filenames=["locales/ru/text.ftl"]
                ),
            ),
            FluentTranslator(
                locale="en",
                translator=FluentBundle.from_files(
                    locale="en-US", filenames=["locales/en/text.ftl"]
                ),
            ),
            FluentTranslator(
                locale="uz",
                translator=FluentBundle.from_files(
                    locale="uz-UZ", filenames=["locales/uz/text.ftl"]
                ),
            ),
        ],
    )
    return translator_hub
