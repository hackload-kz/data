open System.IO

let транслитерировать (имя: string) : string =
    // Define a map for transliteration from Cyrillic to Latin
    let словарьТранслитерации = 
        [ ('а', "a"); ('б', "b"); ('в', "v"); ('г', "g"); ('д', "d")
          ('е', "e"); ('ё', "yo"); ('ж', "zh"); ('з', "z"); ('и', "i")
          ('й', "y"); ('к', "k"); ('л', "l"); ('м', "m"); ('н', "n")
          ('о', "o"); ('п', "p"); ('р', "r"); ('с', "s"); ('т', "t")
          ('у', "u"); ('ф', "f"); ('х', "kh"); ('ц', "ts"); ('ч', "ch")
          ('ш', "sh"); ('щ', "shch"); ('ъ', "'");  // hard sign
          ('ы', "y");  // yeri
          ('ь', "")    // soft sign
          ('э', "e'");  // e
          ('ю', "yu");  // yu
          ('я', "ya");  // yu
          ('ә', "a"); ('ғ', "g"); ('қ', "q"); ('ң', "n"); ('ө', "o")
          ('ұ', "u"); ('ү', "u"); ('Һ', "h") ] |> Map.ofList

    let транслитерированное = 
        имя.ToLower()
        |> Seq.fold (fun акк c ->
            match Map.tryFind c словарьТранслитерации with
            | Some translit -> акк + translit
            | None -> акк + string c) ""
    транслитерированное.ToUpperInvariant()

let транслитерировать_файл имяФайла заголовок =
    let names = 
        File.ReadAllLines имяФайла 
        |> Seq.skip 1
        |> Seq.map (fun line -> line.Split(','))
        |> Seq.map (fun parts -> 
            let transliterated = транслитерировать parts.[1]
            $"{parts[0]},{parts[1]},{transliterated}")
        |> Seq.toList

    File.WriteAllLines(имяФайла, [ заголовок ]  @ names)

транслитерировать_файл "first_names.csv" "Sex,NameKZ,NameEn"
транслитерировать_файл "last_names.csv" "Sex,NameKZ,NameEn"